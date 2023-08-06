import { Widget } from '@lumino/widgets';
import isEqual from "lodash.isequal";

export class EditSettingsWidget extends Widget {
    constructor(atlasId: string) {
        super({ node: EditSettingsWidget.createSettingsWidget(atlasId) });
    }

    private static createSettingsWidget(atlasId: string): HTMLElement {
        const body = document.createElement("div");
        const existingLabel = document.createElement("label");
        existingLabel.textContent = "Atlas ID:";

        const input = document.createElement("input");
        input.classList.add('input')
        input.value = isEqual(atlasId, "") ? "" : atlasId;
        input.placeholder = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";

        body.appendChild(existingLabel);
        body.appendChild(input);
        return body;
    }

    get inputNode() {
        return this.node.getElementsByTagName("input")[0];
    }

    getValue() {
        return this.inputNode.value;
    }
}

export default EditSettingsWidget;