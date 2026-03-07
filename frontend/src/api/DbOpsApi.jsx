import AxiosClient from "./AxiosClient";

const DbOpsApi = {
  listmetadata: (jira_dbdash_uid) => AxiosClient.get(`/dbops/jira/meta/get?jira_dbdash_uid=${jira_dbdash_uid}`),
  createmetadata: (data) => AxiosClient.post("/dbops/jira/meta/create", data),
  updatemetadata: (id, data) => AxiosClient.patch(`/dbops/jira/meta/update/${id}`, data),
  deletemetadata: (jira_id) => AxiosClient.delete(`/dbops/jira/meta/delete/${jira_id}`),
  getmetadatabyid: (jira_id) => AxiosClient.get(`/dbops/jira/meta/getbyid/${jira_id}`),
  getserversall: () => AxiosClient.get(`/dbops/msserver/server/get`),
  getservernmsall: () => AxiosClient.get(`/dbops/msserver/server/get/snm`),
  getserversamountll: (msdbs_id) => AxiosClient.get(`/dbops/msserver/server/mount/${msdbs_id}`),
  createservermount: (data) => AxiosClient.post(`/dbops/msserver/create`, data),
  updateservermount: (msdbs_id, data) => AxiosClient.patch(`/dbops/msserver/server/update/${msdbs_id}`, data),
  deleteservermount: (msdbs_id) => AxiosClient.delete(`/dbops/msserver/server/delete/${msdbs_id}`),  
  deleteserversmount: (msdbsm_id) => AxiosClient.delete(`/dbops/msserver/server/mount/delete/${msdbsm_id}`),  
  getjiraticketdetail: (jira_id, jira_ticket) => AxiosClient.get(`/dbops/jira/ticket/details/${jira_id}/${jira_ticket}`),    
  provisiondb: (exec, payload) => AxiosClient.post(`/dbops/msserver/provision/database?runmode=${exec}`, payload),   
  getalljobs: () => AxiosClient.get(`/dbops/msserver/provision/database/jobs`),  
  getjobbyid: (job_id) => AxiosClient.get(`/dbops/msserver/provision/database/jobs/${job_id}`),    
  getjoblogsbyid: (job_id, sincetime) =>
    AxiosClient.get(
      `/dbops/msserver/provision/database/job/logs/${job_id}`,
      {
        params: sincetime ? { sincetime } : {}
      }
    ),

};

export default DbOpsApi;