import { FunctionComponent } from 'react';
interface Props {
    className?: string;
    isLogScale: boolean;
    onToggleScale: (enabled: boolean) => void;
}
declare const MenuBar: FunctionComponent<Props>;
export default MenuBar;
