export declare const datakinds: readonly ["int", "float", "bool", "str", "array", "datetime", "Mesh", "Sequence1D", "Embedding", "Image", "Audio", "Video", "Category", "Window", "Unknown"];
export type DataKind = typeof datakinds[number];
export interface BaseDataType<K extends DataKind> {
    kind: K;
    optional: boolean;
}
export type IntegerDataType = BaseDataType<'int'>;
export type FloatDataType = BaseDataType<'float'>;
export type BooleanDataType = BaseDataType<'bool'>;
export type StringDataType = BaseDataType<'str'>;
export type ArrayDataType = BaseDataType<'array'>;
export type DateTimeDataType = BaseDataType<'datetime'>;
export type MeshDataType = BaseDataType<'Mesh'>;
export type SequenceDataType = BaseDataType<'Sequence1D'>;
export type ImageDataType = BaseDataType<'Image'>;
export type AudioDataType = BaseDataType<'Audio'>;
export type VideoDataType = BaseDataType<'Video'>;
export type WindowDataType = BaseDataType<'Window'>;
export interface CategoricalDataType extends BaseDataType<'Category'> {
    kind: 'Category';
    categories: Record<string, number>;
    invertedCategories: Record<number, string>;
}
export interface EmbeddingDataType extends BaseDataType<'Embedding'> {
    kind: 'Embedding';
    embeddingLength: number;
}
export type UnknownDataType = BaseDataType<'Unknown'>;
export type DataType = UnknownDataType | IntegerDataType | FloatDataType | BooleanDataType | StringDataType | ArrayDataType | DateTimeDataType | MeshDataType | SequenceDataType | EmbeddingDataType | ImageDataType | AudioDataType | VideoDataType | WindowDataType | CategoricalDataType | NumericalDataType | ScalarDataType;
export declare const isInteger: (type: DataType) => type is IntegerDataType;
export declare const isFloat: (type: DataType) => type is FloatDataType;
export declare const isBoolean: (type: DataType) => type is BooleanDataType;
export declare const isString: (type: DataType) => type is StringDataType;
export declare const isArray: (type: DataType) => type is ArrayDataType;
export declare const isDateTime: (type: DataType) => type is DateTimeDataType;
export declare const isMesh: (type: DataType) => type is MeshDataType;
export declare const isSequence: (type: DataType) => type is SequenceDataType;
export declare const isEmbedding: (type: DataType) => type is EmbeddingDataType;
export declare const isImage: (type: DataType) => type is ImageDataType;
export declare const isAudio: (type: DataType) => type is AudioDataType;
export declare const isVideo: (type: DataType) => type is VideoDataType;
export declare const isWindow: (type: DataType) => type is WindowDataType;
export declare const isCategorical: (type: DataType) => type is CategoricalDataType;
export declare const isUnknown: (type: DataType) => type is UnknownDataType;
export interface NumericalDataType {
    kind: 'int' | 'float';
}
export declare const isNumerical: (type: DataType) => type is NumericalDataType;
export interface ScalarDataType {
    kind: 'int' | 'float' | 'str' | 'bool';
}
export declare const isScalar: (type: DataType) => type is ScalarDataType;
export declare function getNullValue(kind: DataKind): number | boolean | string | null;
