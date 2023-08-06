/*!
 * Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { NotebookPanel } from "@jupyterlab/notebook";
import {
    ApiClient,
    GenerateCompletionsRequest,
    GenerateCompletionsResponse,
    GenerateRecommendationsResponse,
    RecommendationsList,
} from "../client/apiclient";
import {
    getFileContextFromNotebook,
    getFileContextFromEditor,
} from "./extractor";
import { AWS_BUILDER_ID_START_URL, 
    MAX_PAGINATION_CALLS, 
    MAX_RECOMMENDATIONS, 
    LEARN_MORE_NOTIFICATION_URL } from "../utils/constants";
import { message } from "../messages";
import { Signal } from "@lumino/signaling";
import { CodeEditor } from "@jupyterlab/codeeditor";
import {
    CodewhispererServiceInvocation,
    Result,
} from "../telemetry/telemetry.gen";
import { Logger } from '../logging/logger';
import { pino } from 'pino';
import { NotificationManager } from "../notifications/notifications";
import { FileContextMetadata, TriggerMetadata } from "../utils/models";
import { detectCompletionType, getErrorResponseUserMessage, isResponseSuccess } from "../utils/utils";
import { RecommendationStateHandler } from "./recommendationStateHandler";

export class Worker {
    private client: ApiClient;
    private static instance: Worker;
    private _isGetCompletionsRunning: boolean = false;
    private logger: pino.Logger;
    /**
     * This boolean is used to stop subsequent paginated requests when user has rejected/accepted 
     * any completions returned by previous requests.
     */
    public isInvocationCancelled: boolean = false;
    
    private suggestionsWithCodeReferences: Boolean;
    private optOut: Boolean = false;

    public receivedResponseSignal: Signal<any, RecommendationsList>;
    public serviceInvocationSignal: Signal<this, CodewhispererServiceInvocation>;
    public invocationStatusChangedSignal: Signal<any, boolean>;

    public static getInstance(): Worker {
        if (!Worker.instance) {
            Worker.instance = new Worker();
        }
        return Worker.instance;
    }

    private constructor() {
        this.client = new ApiClient();
        this.receivedResponseSignal = new Signal(this);
        this.serviceInvocationSignal = new Signal(this);
        this.invocationStatusChangedSignal = new Signal(this);
        this.logger = Logger.getInstance({
            "name": "codewhisperer",
            "component" : "worker"
        });
    }

    public get isGetCompletionsRunning(): boolean {
        return this._isGetCompletionsRunning
    }

    public set isGetCompletionsRunning(value: boolean) {
        this._isGetCompletionsRunning = value
        this.invocationStatusChangedSignal.emit(value)
    }

    /* Call the generateCompletions API with next Token and emit result
     *  this.isGetCompletionsRunning is used to ensure concurrency <= 1
     */
    async getCompletionsPaginated(
        request: GenerateCompletionsRequest,
        triggerMetadata: TriggerMetadata,
        fileContextMetadata: FileContextMetadata
    ) {
        let responseJson = undefined;
        let requestId = "";
        let sessionId = "";
        let credentialStartUrl = "";
        let page = 0;
        let startTime = undefined;
        let reason = undefined;
        let result: Result = undefined;
        let recommendationCount = 0;
        let shouldRecordServiceInvocation = true;

        if (this._isGetCompletionsRunning) {
            return
        }
        RecommendationStateHandler.instance.rejectRecommendationSignal.emit(-1);
        this.isInvocationCancelled = false;
        while (!this.isInvocationCancelled && page < MAX_PAGINATION_CALLS) {
            this.isGetCompletionsRunning = true;
            try {
                startTime = Date.now();
                const response = await this.client.generateRecommendations(request, this.optOut);
                responseJson = await response.json();
                this.logger.debug("responseJson", responseJson);
                requestId = responseJson["x-amzn-requestid"];
                sessionId = responseJson["x-amzn-sessionid"];
                result = "Succeeded";
            } catch (error) {
                this.logger.error(`Error in calling generateRecommendations API `, error);
                reason = error;
                result = "Failed";
            } finally {
                if (responseJson && !isResponseSuccess(responseJson)) {
                    const errUserMessage = getErrorResponseUserMessage(responseJson);
                    await NotificationManager.getInstance().postNotificationForApiExceptions(
                        errUserMessage,
                        message("codewhisperer_learn_more"),
                        LEARN_MORE_NOTIFICATION_URL,
                    );
                    reason = errUserMessage;
                    if (responseJson["message"] && responseJson["message"].includes("Invalid input data")) {
                        shouldRecordServiceInvocation = false;
                        this.logger.debug("Invalid input data, not recording service invocation");
                    }
                    result = "Failed";
                }

                let recommendations = undefined;
                if (responseJson && isResponseSuccess(responseJson)) {
                    if ("recommendations" in responseJson["data"]) {
                        recommendations = (responseJson["data"] as GenerateRecommendationsResponse).recommendations;
                    } else if ("completions" in responseJson["data"]) {
                        recommendations = (responseJson["data"] as GenerateCompletionsResponse).completions;
                        credentialStartUrl = AWS_BUILDER_ID_START_URL;
                    }
                    if (!this.suggestionsWithCodeReferences) {
                        recommendations = recommendations.filter((r) => !Array.isArray(r.references) || r.references.length === 0);
                    }

                }
                if (recommendations) {
                    this.receivedResponseSignal.emit(recommendations);
                    recommendationCount += recommendations.length > 0 ? recommendations.length : 1;
                    this.logger.debug("successfully received valid recommendations");
                }

                const completionType = detectCompletionType(recommendations);
                if (shouldRecordServiceInvocation) {
                    this.serviceInvocationSignal.emit({
                        codewhispererRequestId: requestId,
                        credentialStartUrl: credentialStartUrl,
                        duration: Date.now() - startTime,
                        reason: reason,
                        result: result,
                        codewhispererCompletionType: completionType,
                        codewhispererTriggerType: triggerMetadata.triggerType,
                        codewhispererAutomatedTriggerType: triggerMetadata.automatedTriggerType,
                        codewhispererSessionId: sessionId,
                        // TODO: sessionID, runtime and runtimeSource
                        codewhispererJupyterLabCellCount: fileContextMetadata.cellCount,
                        codewhispererJupyterLabCellIndex: fileContextMetadata.activeCellIdx,
                        codewhispererJupyterLabCellType: fileContextMetadata.cellType,
                        codewhispererLanguage: triggerMetadata.language,
                        codewhispererLastSuggestionIndex: (result === "Succeeded" && recommendations) ? recommendationCount - 1 : -1,
                        codewhispererCursorOffset: fileContextMetadata.cursorOffset,
                        codewhispererLineNumber: fileContextMetadata.lineNumber,
                    } as CodewhispererServiceInvocation);
                }

                if (result === "Succeeded") {
                    RecommendationStateHandler.instance.updateInvocationMetadata({
                        completionType: completionType,
                        credentialStartUrl: credentialStartUrl,
                        sessionId: sessionId,
                        paginationProgress: recommendationCount,
                        fileContextMetadata: fileContextMetadata,
                        triggerMetadata: triggerMetadata
                    }, requestId, page === 0);
    
                    if (recommendations) {
                        RecommendationStateHandler.instance.addRecommendations(recommendations);
                    }
                }

                if (responseJson && isResponseSuccess(responseJson) && responseJson['data'].nextToken !== '') {
                    request.nextToken = responseJson['data'].nextToken;
                } else {
                    break;
                }
                page++;

            }
        }
        if (this.isInvocationCancelled) {
            RecommendationStateHandler.instance.rejectRecommendationSignal.emit(-1);
        }
        this.isGetCompletionsRunning = false;
        // TODO: add time out
    }

    async getCompletionsPaginatedInNotebookPanel(panel: NotebookPanel, triggerMetadata: TriggerMetadata) {
        const { fileContext, fileContextMetadata } =
            getFileContextFromNotebook(panel);
        let request: GenerateCompletionsRequest = {
            fileContext: fileContext,
            maxResults: MAX_RECOMMENDATIONS,
            referenceTrackerConfiguration: {
                recommendationsWithReferences: this.suggestionsWithCodeReferences ? "ALLOW" : "BLOCK",
            },
            nextToken: "",
        };
        return await this.getCompletionsPaginated(
            request,
            triggerMetadata,
            fileContextMetadata,
        );
    }

    async getCompletionsPaginatedInEditor(
        editor: CodeEditor.IEditor,
        filename: string,
        triggerMetadata: TriggerMetadata
    ) {
        const {fileContext, fileContextMetadata} = getFileContextFromEditor(editor, filename);
        let request: GenerateCompletionsRequest = {
            fileContext: fileContext,
            maxResults: MAX_RECOMMENDATIONS,
            referenceTrackerConfiguration: {
                recommendationsWithReferences: "ALLOW",
            },
            nextToken: "",
        };
        await this.getCompletionsPaginated(
            request,
            triggerMetadata,
            fileContextMetadata
        );
    }

    public setSuggestionsWithCodeReferences(suggestionsWithCodeReferences : boolean): void {
        this.suggestionsWithCodeReferences = suggestionsWithCodeReferences;
    }

    public setOptOut(optOut : boolean): void {
        this.optOut = optOut;
    }
}
