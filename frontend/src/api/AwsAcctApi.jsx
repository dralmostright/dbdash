import AxiosClient from "./AxiosClient";

const AwsAcctApi = {
  listall: () => AxiosClient.get("aws/org/getall"),
  createac: (data) => AxiosClient.post("aws/org/register", data),
  getawsacbyid: (id) => AxiosClient.get(`aws/org/account/${id}`),
  updateac: (aid, data) => AxiosClient.patch(`/aws/org/account/${aid}`, data),
  deleteac: (aid) => AxiosClient.delete(`/aws/org/account/${aid}`)
};

export default AwsAcctApi;