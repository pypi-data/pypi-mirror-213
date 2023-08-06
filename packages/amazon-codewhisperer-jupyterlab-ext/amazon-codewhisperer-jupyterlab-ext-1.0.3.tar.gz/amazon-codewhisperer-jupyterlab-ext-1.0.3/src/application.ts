/*!
 * Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
import { Signal } from "@lumino/signaling";
import { AutoTrigger } from "./autotrigger/autotrigger";
import { Worker } from "./recommendation/worker";
import { AuthManager } from "./auth/authManager";
import { requestAPI } from "./handler";
import { getResponseData } from "./utils/utils";
import { HttpStatusCode } from "./utils/constants";
import { NotificationManager } from "./notifications/notifications";
import {  UPDATE_NOTIFICATION_URL } from "./utils/constants";
import { message } from "./messages";
import { IStateDB } from "@jupyterlab/statedb";
import { JupyterFrontEnd } from "@jupyterlab/application";

export class Application {
    private static instance: Application;
    public loadStateSignal: Signal<any, any>;
    private _environment: Environment = undefined;
    public stateDB: IStateDB;
    public jupyterApp: JupyterFrontEnd;

    public static getInstance(): Application {
        if (!Application.instance) {
            Application.instance = new Application()
        }
        return Application.instance;
    }

    private constructor() {
        this.loadStateSignal = new Signal(this);
    }

    private async _fetchEnvironment() {
        const getEnvironmentResponse = await requestAPI<Response>('get_environment')
        if (getEnvironmentResponse.status !== HttpStatusCode.OK) return;
        const getEnvironmentResponseJson = await getEnvironmentResponse.json()
        this._environment = getResponseData(getEnvironmentResponseJson)['environment'];
        const versionNotificaion = getResponseData(getEnvironmentResponseJson)['version_notification'];
        const latestVersion = getResponseData(getEnvironmentResponseJson)['latest_version'];
        if(versionNotificaion) {
            NotificationManager.getInstance().postNotificationForUpdateInformation(
                versionNotificaion,
                latestVersion,
                message("codewhisperer_update_now"),
                UPDATE_NOTIFICATION_URL
            ).then();
        }
    }

    public isJupyterOSS(): boolean {
        return this._environment === Environment.JUPYTER_OSS;
    }

    public isSageMakerStudio(): boolean {
        return this._environment === Environment.SM_STUDIO;
    }

    // Initialize all the application singletons here
    public async loadServices(stateDB: IStateDB, jupyterApp: JupyterFrontEnd) {
        this.stateDB = stateDB;
        this.jupyterApp = jupyterApp;

        await this._fetchEnvironment()

        Worker.getInstance();
        AutoTrigger.getInstance();
        AuthManager.getInstance();
    }
}

enum Environment {
    JUPYTER_OSS = 'Jupyter OSS',
    SM_STUDIO = 'SageMaker Studio'
}
