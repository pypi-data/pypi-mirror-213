import { Panel } from '@lumino/widgets';
import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { JupyterYModel } from 'yjs-widgets';
import { JupyterCadModel } from '../model';
export interface ICommMetadata {
    create_ydoc: boolean;
    path: string;
    format: string;
    contentType: string;
    ymodel_name: string;
}
export declare const CLASS_NAME = "jupytercad-notebook-widget";
export declare class YJupyterCADModel extends JupyterYModel {
    jupyterCADModel: JupyterCadModel;
}
export declare class YJupyterCADLuminoWidget extends Panel {
    constructor(model: JupyterCadModel);
    onResize: () => void;
    private _jcadWidget;
}
export declare const yJupyterCADWidgetPlugin: JupyterFrontEndPlugin<void>;
