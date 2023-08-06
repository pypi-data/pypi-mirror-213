import { ReactWidget } from "@jupyterlab/apputils";
import React, { useState } from 'react';
import { HTMLSelect } from '@jupyterlab/ui-components';
import { ISignal, Signal } from '@lumino/signaling';

interface IAtlasIdProps {
    atlasId: string | undefined;
    signal: Signal<ChatlasDropdownWidget, string>;
};

const ChatlasDropdownMenuComponent = (info: IAtlasIdProps): JSX.Element => {
    const [selected, setSelected] = useState<string>("");

    function _onSelect(event: React.ChangeEvent<HTMLSelectElement>): void {
        event.preventDefault();
        const newValue = event.target.value;
        setSelected(newValue)
        info.signal.emit(newValue)
        console.log(`Selected Option => ${newValue}`)
    }
    console.log(`Info => ${info.atlasId}`)
    const TOOLBAR_CELLTYPE_DROPDOWN_CLASS = 'jp-Notebook-toolbarCellTypeDropdown';
    const options = [
        { value: 'set', label: 'Add/Modify Atlas Id' },
        { value: 'delete', label: 'Remove Chatlas' }
    ];

    return (
        <HTMLSelect
            className={TOOLBAR_CELLTYPE_DROPDOWN_CLASS}
            onChange={_onSelect}
            value={selected}
            aria-label='Chatlas Actions'
            title='Chatlas Actions'
        >
            <option value="" disabled selected>Chatlas Actions</option>
            {options.map((item, _) => {
                return <option value={item.value}>{item.label}</option>
            })}
        </HTMLSelect>
    )
}


export class ChatlasDropdownWidget extends ReactWidget {
    private _signal = new Signal<this, string>(this);

    public get menuOptionChanged(): ISignal<this, string> {
        return this._signal;
    }

    info: IAtlasIdProps = {
        atlasId: '',
        signal: this._signal
    }

    constructor(atlasId: string | undefined) {
        super()
        this.info.atlasId = atlasId;
    }

    render(): JSX.Element {
        return <ChatlasDropdownMenuComponent {...this.info} />;
    }

}