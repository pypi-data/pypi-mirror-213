import * as React from 'react';
import { DataColumn, LensKey } from '../types';
interface Props {
    view: LensKey;
    columns: DataColumn[];
    rowIndex: number;
    syncKey: string;
}
declare const ViewFactory: React.FunctionComponent<Props>;
export default ViewFactory;
