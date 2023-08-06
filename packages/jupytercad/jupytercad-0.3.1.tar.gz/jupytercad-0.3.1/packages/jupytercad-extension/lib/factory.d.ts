import { ABCWidgetFactory, DocumentRegistry } from '@jupyterlab/docregistry';
import { CommandRegistry } from '@lumino/commands';
import { JupyterCadModel } from './model';
import { IJupyterCadTracker } from './token';
import { JupyterCadWidget } from './widget';
interface IOptios extends DocumentRegistry.IWidgetFactoryOptions {
    tracker: IJupyterCadTracker;
    commands: CommandRegistry;
    backendCheck?: () => boolean;
}
export declare class JupyterCadWidgetFactory extends ABCWidgetFactory<JupyterCadWidget, JupyterCadModel> {
    constructor(options: IOptios);
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    protected createNewWidget(context: DocumentRegistry.IContext<JupyterCadModel>): JupyterCadWidget;
    private _commands;
    private _backendCheck?;
}
export {};
