import AxiosClient from "./AxiosClient";

const UsersApi = {
  listall: () => AxiosClient.get("/auth/allusers"),
  create: (data) => AxiosClient.post("/auth/register", data),
  update: (id, data) => AxiosClient.put(`/users/${id}`, data),
  remove: (id) => AxiosClient.delete(`/auth/user/remove?uid=${id}`),
  updateuser: (uid, data) => AxiosClient.patch(`/auth/user/update?uid=${uid}`, data),
  getuser: (uid) => AxiosClient.get(`/auth/user/details?uid=${uid}`),
  changedp: (uid,data) => AxiosClient.post(`/auth/user/change/displaypic?uid=${uid}`,data , {headers: { "Content-Type": "multipart/form-data" },}),
  changepassword: (uid,data) => AxiosClient.patch(`/auth/user/change/password?uid=${uid}`,data),
  changeinfo: (uid,data) => AxiosClient.patch(`/auth/user/change/basicinfo?uid=${uid}`,data),
};

export default UsersApi;