import AxiosClient from "./AxiosClient";


const AuthApi = {
  register: (data) => AxiosClient.post("/auth/register", data),
  login: (data) => AxiosClient.post("/auth/login", data),
  getProfile: () => AxiosClient.get("/auth/me"),
  refresh: () =>
    AxiosClient.post("/auth/refresh_token", {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("refresh_token")}`,
      },
    }),
};

export default AuthApi;
