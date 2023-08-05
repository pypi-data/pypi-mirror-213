import * as React from 'react';
import { VariableSizeGrid as Grid } from 'react-window';
interface Props {
    height: number;
    width: number;
    columnWidth: (index: number) => number;
    onStartResize: (columnIndex: number) => void;
    resizedIndex?: number;
}
declare const _default: React.ForwardRefExoticComponent<Props & React.RefAttributes<Grid<any>>>;
export default _default;
