
/**
 * Check if a value is null, undefined, "undefined", "null", "false" or an empty string
 * 
 * @param value
 * @returns 
 */
export function isNone(value: any): boolean {
    if (typeof value === "string") value = value.trim()
    return (
        value === null ||
        value === undefined ||
        value === "undefined" ||
        value === "null" ||
        value === "false" ||
        value === ""
    );
}