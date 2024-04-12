import type { APIResponse } from '~/typings'
const decoder = new TextDecoder()

export async function readStream(reader: ReadableStreamDefaultReader | null, callback: (data: APIResponse) => void, fallback?: (text: string) => void) {
    if (!reader) throw new Error('Reader is not defined')
    const { done, value } = await reader.read()

    if (done) return

    const text = decoder.decode(value)

    try {
        text.replace(/\n/g, '')
            .replace(/}{/g, '}\n{')
            .split('\n')
            .filter(line => line.trim() !== '')
            .map(line => JSON.parse(line))
            .forEach(callback)
    } catch (e) {
        console.warn(e)
        if (fallback) fallback(text)
    }

    return readStream(reader, callback, fallback)
}
