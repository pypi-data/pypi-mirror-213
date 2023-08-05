import { FunctionComponent } from 'react';
import type { GridChildComponentProps as CellProps } from 'react-window';
type ItemData = {
    onStartResize: (columnIndex: number) => void;
    resizedIndex?: number;
};
type Props = CellProps<ItemData>;
declare const HeaderCell: FunctionComponent<Props>;
export default HeaderCell;
