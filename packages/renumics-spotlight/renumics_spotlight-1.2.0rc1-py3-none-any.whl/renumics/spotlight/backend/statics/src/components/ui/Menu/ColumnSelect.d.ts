/// <reference types="react" />
export interface Props {
    title: string;
    selected?: string;
    selectableColumns: string[];
    onChangeColumn: (keys: string) => void;
}
declare const _default: import("react").NamedExoticComponent<Props>;
export default _default;
