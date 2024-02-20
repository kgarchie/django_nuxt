import {type UserState} from "~/typings";

export const useUser = () => useState<UserState>('user', () => {
    return {} as UserState
})
