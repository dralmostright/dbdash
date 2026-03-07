import AxiosClient from "./AxiosClient";

const RdsApi = {
  getRdsTotalCount: () => AxiosClient.get("/aws/rds/total"),
  getRdsTotalUpCount: () => AxiosClient.get("/aws/rds/total?status=up"),
  getRdsTotaldownCount: () => AxiosClient.get("/aws/rds/total?status=down"),
  getAccountRdsCountPerDay: () => AxiosClient.get("aws/rds/account/count?interval=dd&duration=30"),
  getRdsEngineCount: () => AxiosClient.get("aws/rds/engine/count"),
  getRdsAzAccountCount: () => AxiosClient.get("aws/rds/engine/az-count"),
  getRdsEngineAccountCount: () => AxiosClient.get("aws/rds/engine/ver-count"),
  getRdsCreatedCount: () => AxiosClient.get("aws/rds/created/count?interval=dd&duration=30"),
  getRdsList: (viewMode) => AxiosClient.get(`aws/rds/getall?viewmode=${viewMode}`),
  getRdsInstanceDetail: (riid) => AxiosClient.get(`aws/rds/instance/${riid}`),
  getRdsHwDetail: (riid) => AxiosClient.get(`aws/rds/engine/hw-details/${riid}`),
  getRdsEol: (eoltype) => AxiosClient.get(`aws/rds/engine/eol?eoltype=${eoltype}`),
  getRdsSecRules: (riid) => AxiosClient.get(`aws/rds/engine/secrules?riid=${riid}`),
  getRdsInstParams: (riid) => AxiosClient.get(`aws/rds/engine/params?riid=${riid}`),
  getRdsEolMajorDetail: (engine) => AxiosClient.get(`aws/rds/engine/eol/detail/major?engine=${engine}`),
  getRdsEolMinorDetail: (engine) => AxiosClient.get(`aws/rds/engine/eol/detail/minor?engine=${engine}`),
  refreshRdsEolData: (engine,version) => AxiosClient.get(`aws/rds/engine/eol/refresh?engine=${engine}&version=${version}`),
  getRdsHwTypes: (hwtype) => AxiosClient.get(`aws/rds/engine/hw/${hwtype}-types/detail`), 
  refreshRdsHwTypes: (hwtype) => AxiosClient.get(`aws/rds/engine/hw/${hwtype}-types/refresh`), 
  getRdsAccountEngineCount: () => AxiosClient.get(`aws/rds/account/engine/count`), 
  getRdsRecentActivity: () => AxiosClient.get(`aws/rds/engine/recent/activity?duration=30`), 
  getRdsEolMinorList: () => AxiosClient.get(`/aws/rds/getall/minoreol`),
  getRdsEolMajorList: () => AxiosClient.get(`/aws/rds/getall/majoreol`),
};

export default RdsApi;