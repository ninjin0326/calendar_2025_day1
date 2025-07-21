type ApiErrorCode = string;

interface ApiErrorResponse {
  message: string;
}

class ApiRequestError extends Error {
  constructor(public code: ApiErrorCode, public body?: ApiErrorResponse) {
    super(`API Request Error: ${code}`);
    this.name = "ApiRequestError";
  }
}

/**
 * 400番代、500番代のエラーをハンドリングするfetch関数
 * @returns null が返ってくる場合はステータスコードのみが帰ってきた場合
 */
export const fetchApi = <T>(
  url: RequestInfo,
  options: RequestInit
): Promise<T | null> => {
  const credentials = btoa(
    `${import.meta.env.VITE_USERNAME}:${import.meta.env.VITE_PASSWORD}`
  );
  const optionsWithCredentials: RequestInit = {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Basic ${credentials}`,
    },
  };
  return fetch(url, optionsWithCredentials)
    .catch((e: Error) => {
      console.error(e);
      throw new Error(e.message);
    })
    .then(handleErrors)
    .then((res: Response) => {
      if (res.headers.get("content-type")?.includes("application/json")) {
        return res.json() as Promise<T>;
      }
      return null;
    })
    .catch((e: Error) => {
      console.error(e);
      throw new Error(e.message);
    });
};

const handleErrors = async (res: Response | void): Promise<Response> => {
  if (!res) throw new Error("Request was aborted");
  if (res.ok) return res;

  let body: ApiErrorResponse | undefined = undefined;
  try {
    body = (await res.json()) as ApiErrorResponse;
  } catch {
    // Non json response
  }

  switch (res.status) {
    case 400:
      throw new ApiRequestError("INVALID_TOKEN", body);
    case 401:
      throw new ApiRequestError("UNAUTHORIZED", body);
    case 403:
      throw new ApiRequestError("FORBIDDEN", body);
    case 500:
      throw new ApiRequestError("INTERNAL_SERVER_ERROR", body);
    case 502:
      throw new ApiRequestError("BAD_GATEWAY", body);
    case 404:
      throw new ApiRequestError("NOT_FOUND", body);
    default:
      throw new ApiRequestError("UNHANDLED_ERROR", body);
  }
};

export const getBackendUrl = (path: string): URL => {
  const urlString = import.meta.env.VITE_BACKEND_URL;
  if (!urlString) {
    throw new Error("VITE_BACKEND_URL is not defined");
  }
  const url = new URL(urlString);
  url.pathname = path;
  return url;
};
