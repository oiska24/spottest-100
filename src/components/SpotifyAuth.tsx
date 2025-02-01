import React, { useEffect, useState } from 'react';

const clientId: string = '8810b93c97364706a68dba1d23e0f640';
const redirectUrl: string = 'http://localhost:8080';
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

interface UserPlaylists {
    href: string;
    limit: number;
    next: string;
    offset: number;
    previous: string;
    total: number;
    items: Array<any>;
}

const SpotifyAuth: React.FC = () => {
    const [currentToken, setCurrentToken] = useState<TokenResponse | null>(null);
    const [userData, setUserData] = useState<UserData | null>(null);
    const [userPlaylists, setUserPlaylists] = useState<UserPlaylists | null>(null);

    useEffect(() => {
        const args = new URLSearchParams(window.location.search);
        const code = args.get('code');

        if (code) {
            getToken(code).then(token => {
                saveToken(token);
                setCurrentToken(token);
                window.history.replaceState({}, document.title, window.location.pathname);
            });
        } else if (localStorage.getItem('access_token')) {
            const token = {
                access_token: localStorage.getItem('access_token')!,
                refresh_token: localStorage.getItem('refresh_token')!,
                expires_in: parseInt(localStorage.getItem('expires_in')!),
            };
            setCurrentToken(token);
        }
    }, []);

    useEffect(() => {
        if (currentToken) {
            getUserData().then(data => setUserData(data));
            getUserPlaylists().then(playlists => setUserPlaylists(playlists));
        }
    }, [currentToken]);

    const saveToken = (token: TokenResponse) => {
        localStorage.setItem('access_token', token.access_token);
        localStorage.setItem('refresh_token', token.refresh_token);
        localStorage.setItem('expires_in', token.expires_in.toString());
    };

    const redirectToSpotifyAuthorize = async () => {
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

        const authUrl = new URL(authorizationEndpoint);
        const params = {
            response_type: 'code',
            client_id: clientId,
            scope: scope,
            code_challenge_method: 'S256',
            code_challenge: code_challenge_base64,
            redirect_uri: redirectUrl,
        };

        authUrl.search = new URLSearchParams(params).toString();
        window.location.href = authUrl.toString();
    };

    const getToken = async (code: string): Promise<TokenResponse> => {
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
                code_verifier: code_verifier!,
            }),
        });

        return await response.json();
    };

    const getUserData = async (): Promise<UserData> => {
        const response = await fetch("https://api.spotify.com/v1/me", {
            method: 'GET',
            headers: { 'Authorization': 'Bearer ' + currentToken?.access_token },
        });

        return await response.json();
    };

    const getUserPlaylists = async (): Promise<UserPlaylists> => {
        const response = await fetch("https://api.spotify.com/v1/playlists", {
            method: 'GET',
            headers: { 'Authorization': 'Bearer ' + currentToken?.access_token },
        });

        return await response.json();
    };

    const handleLoginClick = async () => {
        await redirectToSpotifyAuthorize();
    };

    const handleLogoutClick = () => {
        localStorage.clear();
        setCurrentToken(null);
        window.location.href = redirectUrl;
    };

    return (
        <div>
            {!currentToken ? (
                <button onClick={handleLoginClick}>Login with Spotify</button>
            ) : (
                <div>
                    <button onClick={handleLogoutClick}>Logout</button>
                    {userData && (
                        <div>
                            <h1>Welcome, {userData.display_name}</h1>
                            <p>Email: {userData.email}</p>
                        </div>
                    )}
                    {userPlaylists && (
                        <div>
                            <h2>Your Playlists</h2>
                            <ul>
                                {userPlaylists.items.map((playlist, index) => (
                                    <li key={index}>{playlist.name}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default SpotifyAuth;