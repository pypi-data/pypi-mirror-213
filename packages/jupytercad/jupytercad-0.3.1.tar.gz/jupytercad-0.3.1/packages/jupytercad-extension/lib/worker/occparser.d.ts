import { IDict, IParsedShape } from '../types';
import { IJCadObject } from '../_interface/jcad';
import { IOperatorFuncOutput } from './types';
interface IShapeList {
    shapeData: IOperatorFuncOutput;
    jcObject: IJCadObject;
}
export declare class OccParser {
    private _shapeList;
    private _occ;
    private _showEdge;
    constructor(shapeList: IShapeList[]);
    execute(): IDict<IParsedShape>;
    private _build_wire_mesh;
    private _build_face_mesh;
    private _build_edge_mesh;
}
export {};
