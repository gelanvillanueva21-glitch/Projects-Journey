type ReadonlyCopy<T> = {
    readonly [K in keyof T]: T[K];
};
type Result = ReadonlyCopy<{ name: string }>;

const result: Result = { name: "Gelan" }

console.log(result);
