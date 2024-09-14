/**
 * This is an example of a basic node.js script that performs
 * the Authorization Code with PKCE oAuth2 flow to authenticate 
 * against the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
 * Converted to typescript
 */

export {}; // Make this file a module

const clientId: string = '8810b93c97364706a68dba1d23e0f640'; // your clientId
const redirectUrl: string = 'http://localhost:8080';        // your redirect URL - must be localhost URL and/or HTTPS

const authorizationEndpoint: string = "https://accounts.spotify.com/authorize";
const tokenEndpoint: string = "https://accounts.spotify.com/api/token";
const scope: string = 'user-read-private user-read-email';

interface TokenResponse {
    access_token: string;
    refresh_token: string;
    expires_in: number;
}
  
interface UserData {
    display_name: string;
    email: string;
}

// Data structure that manages the current active token, caching it in localStorage
const currentToken = {
    get access_token(): string | null { return localStorage.getItem('access_token'); },
    get refresh_token(): string | null { return localStorage.getItem('refresh_token'); },
    get expires_in(): string | null { return localStorage.getItem('refresh_in'); },
    get expires(): string | null { return localStorage.getItem('expires'); },

    save: function (response: TokenResponse): void {
        const { access_token, refresh_token, expires_in } = response;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('expires_in', expires_in.toString());

        const now = new Date();
        const expiry = new Date(now.getTime() + (expires_in * 1000));
        localStorage.setItem('expires', expiry.toISOString());
    }
};

// On page load, try to fetch auth code from current browser search URL
const args = new URLSearchParams(window.location.search);
const code: string | null = args.get('code');

// If we find a code, we're in a callback, do a token exchange
if (code) {
    (async () => {
        const token: TokenResponse = await getToken(code);
        currentToken.save(token);
    })();

    // Remove code from URL so we can refresh correctly.
    const url = new URL(window.location.href);
    url.searchParams.delete("code");

    const updatedUrl = url.search ? url.href : url.href.replace('?', '');
    window.history.replaceState({}, document.title, updatedUrl);
}

// If we have a token, we're logged in, so fetch user data and render logged in template
if (currentToken.access_token) {
    (async () => {
        const userData: UserData = await getUserData();
        renderTemplate("main", "logged-in-template", userData);
        renderTemplate("oauth", "oauth-template", currentToken);
    })();
}

// Otherwise we're not logged in, so render the login template
if (!currentToken.access_token) {
    renderTemplate("main", "login");
}

async function redirectToSpotifyAuthorize(): Promise<void> {
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const randomValues = crypto.getRandomValues(new Uint8Array(64));
    const randomString = randomValues.reduce((acc, x) => acc + possible[x % possible.length], "");

    const code_verifier = randomString;
    const data = new TextEncoder().encode(code_verifier);
    const hashed = await crypto.subtle.digest('SHA-256', data);

    const code_challenge_base64 = btoa(String.fromCharCode(...new Uint8Array(hashed)))
        .replace(/=/g, '')
        .replace(/\+/g, '-')
        .replace(/\//g, '_');

    window.localStorage.setItem('code_verifier', code_verifier);

    const authUrl = new URL(authorizationEndpoint)
    const params = {
        response_type: 'code',
        client_id: clientId,
        scope: scope,
        code_challenge_method: 'S256',
        code_challenge: code_challenge_base64,
        redirect_uri: redirectUrl,
    };

    authUrl.search = new URLSearchParams(params).toString();
    window.location.href = authUrl.toString(); // Redirect the user to the authorization server for login
}

// Soptify API Calls
async function getToken(code: string): Promise<TokenResponse> {
    const code_verifier = localStorage.getItem('code_verifier');

    const response = await fetch(tokenEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            client_id: clientId,
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: redirectUrl,
            code_verifier: code_verifier,
        }),
    });

    return await response.json();
}

async function refreshToken(): Promise<TokenResponse> {
    const response = await fetch(tokenEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            client_id: clientId,
            grant_type: 'refresh_token',
            refresh_token: currentToken.refresh_token
        }),
    });

    return await response.json();
}

async function getUserData(): Promise<UserData> {
    const response = await fetch("https://api.spotify.com/v1/me", {
        method: 'GET',
        headers: { 'Authorization': 'Bearer ' + currentToken.access_token },
    });

    return await response.json();
}

// Click handlers
async function loginWithSpotifyClick(): Promise<void> {
    await redirectToSpotifyAuthorize();
}

async function logoutClick(): Promise<void> {
    localStorage.clear();
    window.location.href = redirectUrl;
}

async function refreshTokenClick(): Promise<void> {
    const token = await refreshToken();
    currentToken.save(token);
    renderTemplate("oauth", "oauth-template", currentToken);
}

// HTML Template Rendering with basic data binding - demoware only.
function renderTemplate(targetId: string, templateId: string, data: any = null): void {
    const template = document.getElementById(templateId) as HTMLTemplateElement;
    const clone = template.content.cloneNode(true) as DocumentFragment;

    const elements = clone.querySelectorAll("*");
    elements.forEach(ele => {
        const bindingAttrs = [...ele.attributes].filter(a => a.name.startsWith("data-bind"));

        bindingAttrs.forEach(attr => {
            const target = attr.name.replace(/data-bind-/, "").replace(/data-bind/, "");
            const targetType = target.startsWith("onclick") ? "HANDLER" : "PROPERTY";
            const targetProp = target === "" ? "innerHTML" : target;

            const prefix = targetType === "PROPERTY" ? "data." : "";
            const expression = prefix + attr.value.replace(/;\n\r\n/g, "");

            // Maybe use a framework with more validation here ;)
            try {
                ele[targetProp] = targetType === "PROPERTY" ? eval(expression) : () => { eval(expression) };
                ele.removeAttribute(attr.name);
            } catch (ex) {
                console.error(`Error binding ${expression} to ${targetProp}`, ex);
            }
        });
    });

    const target = document.getElementById(targetId);
    if (target) {
        target.innerHTML = "";
        target.appendChild(clone);
    }
}
