import * as React from 'react';
import { FunctionComponent } from 'react';
import { DataColumn, IndexArray } from '../../types';
type ColumnContextState = {
    columns: DataColumn[];
    columnVisibilities: Map<string, boolean>;
    setColumnVisibilities: React.Dispatch<React.SetStateAction<Map<string, boolean>>>;
    rowIndices: IndexArray;
};
export declare const DataContext: React.Context<ColumnContextState>;
export declare const DataProvider: FunctionComponent<{
    children: React.ReactNode;
}>;
export {};
