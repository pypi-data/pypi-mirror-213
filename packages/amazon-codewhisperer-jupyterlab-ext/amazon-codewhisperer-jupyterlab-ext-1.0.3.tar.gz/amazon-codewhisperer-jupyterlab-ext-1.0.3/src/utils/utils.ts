import { CodewhispererCompletionType } from "../telemetry/telemetry.gen";
import { RecommendationsList } from "../client/apiclient";
import { ReadonlyPartialJSONObject } from "@lumino/coreutils";
import { Application } from "../application";
/**
 * @param f callback
 * @param wait milliseconds
 * @param abortValue if has abortValue, promise will reject it if
 * @returns Promise
 */
export function debouncePromise<T extends (...args: any[]) => any>(
    fn: T,
    wait: number,
    abortValue: any = undefined
) {
    let cancel = () => {
        // do nothing
    };
    type Awaited<T> = T extends PromiseLike<infer U> ? U : T
    type ReturnT = Awaited<ReturnType<T>>;
    const wrapFunc = (...args: Parameters<T>): Promise<ReturnT> => {
        cancel();
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => resolve(fn(...args)), wait);
            cancel = () => {
                clearTimeout(timer);
                if (abortValue !== undefined) {
                    reject(abortValue);
                }
            };
        });
    };
    return wrapFunc;
}



export function sleep(duration: number = 0): Promise<void> {
    const schedule = setTimeout
    return new Promise(r => schedule(r, Math.max(duration, 0)))
}

export function detectCompletionType(recommendations: RecommendationsList): CodewhispererCompletionType {
    if (
        recommendations &&
        recommendations.length > 0) {
        if (recommendations[0].content.search("\n") !== -1) {
            return "Block";
        } else {
            return "Line";
        }
    } else {
        return undefined;
    }
}

// TODO: make loadState, saveState, removeState into Application as a centralized place to manage state
// Use `await loadState(id)` to get the actual value
export async function loadState(id: string): Promise<any | undefined> {
    try {
        const value = await Application.getInstance().stateDB.fetch(id);
        return await value;
    } catch (error) {
        return undefined;
    }
}

export async function saveState(id: string, value: any) {
    try {
        await Application.getInstance().stateDB.save(id, value);
    } catch (error) {
    }
}

export async function removeState(id: string) {
    try {
        await Application.getInstance().stateDB.remove(id);
    } catch (error) {
    }
}

export function isResponseSuccess(json: ReadonlyPartialJSONObject): boolean {
    return json['status'] === 'SUCCESS'
}

export function getResponseData(json: ReadonlyPartialJSONObject): any {
    return json['data']
}

export function getErrorResponseUserMessage(json: ReadonlyPartialJSONObject): any {
    if (json["error_info"]) {
        const errorInfo = json["error_info"] as ReadonlyPartialJSONObject;
        return errorInfo["user_message"]
    } else if (json["message"]) {
        return (json["message"] as ReadonlyPartialJSONObject)
    } else {
        return "unknown error user message";
    }   
}
