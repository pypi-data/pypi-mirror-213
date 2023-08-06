import { TopoDS_Shape } from '@jupytercad/jupytercad-opencascade';
import { IJCadContent, Parts, IShapeMetadata } from '../_interface/jcad';
import { IDict } from '../types';
export declare function expand_operator(name: Parts | 'BrepFile', args: any, content: IJCadContent): IDict;
export declare function shape_meta_data(shape: TopoDS_Shape): IShapeMetadata;
export declare function operatorCache<T>(name: Parts | 'BrepFile', ops: (args: T, content: IJCadContent) => TopoDS_Shape | undefined): (args: T, content: IJCadContent) => {
    occShape: TopoDS_Shape;
    metadata?: IShapeMetadata | undefined;
} | undefined;
