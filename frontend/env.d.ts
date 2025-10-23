interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_APP_AUTH_KEY: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
