import { AutoTrigger } from "../../autotrigger/autotrigger";
import { IObservableString } from "@jupyterlab/observables";

jest.mock("@jupyterlab/apputils");
jest.mock("@jupyterlab/ui-components");
jest.mock("@jest/transform");
jest.mock("../../logging/logger");
jest.mock("../../inline/inline");

let autoTrigger = new AutoTrigger();
let changeArgs: IObservableString.IChangedArgs = {
    type: "insert",
    start: 0,
    end: 0,
    value: "a",
};

describe("AutoTrigger tests", () => {
    beforeEach(() => {
        autoTrigger = new AutoTrigger();
    });

    test("should trigger on idle time", async () => {
        changeArgs.type = "insert";
        changeArgs.value = "a";
        autoTrigger.lastKeyStrokeTime = performance.now() - 3000;

        const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
        expect(returnedValue.autoTriggerType).toBe("IdleTime");
        expect(returnedValue.triggerCharacter).toBeUndefined();
    });

    test("should not trigger on idle time", async () => {
        changeArgs.type = "insert";
        changeArgs.value = "a";
        autoTrigger.lastKeyStrokeTime = performance.now();

        const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
        expect(returnedValue.autoTriggerType).toBe(undefined);
        expect(returnedValue.triggerCharacter).toBeUndefined();
    });

    test("should trigger on new line", async () => {
        changeArgs.type = "insert";
        changeArgs.value = "\n";

        const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
        expect(returnedValue.autoTriggerType).toBe("Enter");
        expect(returnedValue.triggerCharacter).toBeUndefined();
    });

    test("should trigger on special character", async () => {
        changeArgs.type = "insert";
        changeArgs.value = "(";

        const returnedValue = autoTrigger.shouldAutoTrigger(changeArgs);
        expect(returnedValue.autoTriggerType).toBe("SpecialCharacters");
        expect(returnedValue.triggerCharacter).toBe("(");
    });
});
