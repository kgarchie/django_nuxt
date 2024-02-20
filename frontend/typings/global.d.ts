import type { RuntimeConfig } from "nuxt/schema";

declare global {
    namespace NodeJS {
        interface Global{
            $config: RuntimeConfig
        }
    }

    var $config: RuntimeConfig
}