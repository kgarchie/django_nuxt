export type APIResponse = {
    statusCode: number,
    body?: any
}

export type UserState = {
    email: string;
    is_admin: boolean;
    token: string;
}