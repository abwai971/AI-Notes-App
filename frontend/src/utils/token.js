const ACCESS_TOKEN = "access_token";
const REFRESH_TOKEN = "refresh_token";

export function saveTokens(access, refresh) {
    localStorage.setItem(ACCESS_TOKEN, access);
    localStorage.setItem(REFRESH_TOKEN, refresh);
}

export function getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN);
}

export function getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN);
}

export function removeTokens() {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
}

export function isAuthenticated() {
    return !!getAccessToken();
}