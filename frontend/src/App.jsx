import { Routes, Route } from "react-router";
import { DashBoard } from "./pages/dashboard/DashBoard";
import { LoginPage } from "./pages/login/LoginPage";
import { RegisterPage } from "./pages/register/RegisterPage";
import { ListAwsAccounts } from "./pages/awsaccts/ListAwsAccounts";
import { AuthProvider } from "./context/AuthProvider";
import { ListUsers } from "./pages/users/ListUsers";
import AddUser from "./pages/users/AddUser";
import ProtectedRoute from "./routes/ProtectedRoute";
import { UserProfile } from "./pages/users/UserProfile";
import AddAwsAccount from "./pages/awsaccts/AddAwsAccount";
import EditAwsAccount from "./pages/awsaccts/EditAwsAccount";
import Page404 from "./pages/Page404";
import { BrowseInstance } from "./pages/rdsinsts/BrowseInstance";
import { ListRdsInstance } from "./pages/rdsinsts/ListRdsInstance";
import { ViewRdsDetails } from "./pages/rdsinsts/ViewRdsDetails";
import { EditUser } from "./pages/users/EditUser";
import { RdsEol } from "./pages/rdseol/RdsEol";
import { RdsInstType } from "./pages/rdstypes/RdsInstType";
import { ListJiraMeta } from "./pages/dbops/ListJiraMeta";
import { CreateJiraMeta } from "./pages/dbops/CreateJiraMeta";
import { EditJiraMeta } from "./pages/dbops/EditJiraMeta";
import { CreateMSServer } from "./pages/dbops/CreateMSServer";
import { ListMSServer } from "./pages/dbops/ListMSServer";
import { ViewMSDetails } from "./pages/dbops/ViewMSDetails";
import { EditMSServer } from "./pages/dbops/EditMSServer";
import CreateMSServerWizard from "./pages/dbops/CreateMSServerWizard";
import { ListJobs } from "./pages/dbops/ListJobs";
import { ViewJobProgress } from "./pages/dbops/ViewJobProgress";

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/auth/login" element={<LoginPage />}></Route>
        <Route path="/auth/register" element={<RegisterPage />}></Route>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashBoard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/listallusers"
          element={
            <ProtectedRoute>
              <ListUsers />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/adduser"
          element={
            <ProtectedRoute>
              <AddUser />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/edit-user/:uid"
          element={
            <ProtectedRoute>
              <EditUser />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/profile"
          element={
            <ProtectedRoute>
              <UserProfile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/aws/accounts"
          element={
            <ProtectedRoute>
              <ListAwsAccounts />
            </ProtectedRoute>
          }
        />
        <Route
          path="/aws/add-account"
          element={
            <ProtectedRoute>
              <AddAwsAccount />
            </ProtectedRoute>
          }
        />
        <Route
          path="/aws/add-account"
          element={
            <ProtectedRoute>
              <AddAwsAccount />
            </ProtectedRoute>
          }
        />
        <Route
          path="/aws/edit-account/:aid"
          element={
            <ProtectedRoute>
              <EditAwsAccount />
            </ProtectedRoute>
          }
        />
        <Route
          path="/aws/rds/browse"
          element={
            <ProtectedRoute>
              <BrowseInstance />
            </ProtectedRoute>
          }
        />
        <Route
          path="/aws/rds/list-rds/:viewMode"
          element={
            <ProtectedRoute>
              <ListRdsInstance />
            </ProtectedRoute>
          }
        />
        <Route
          path="/aws/rds/eol/:viewMode"
          element={
            <ProtectedRoute>
              <RdsEol />
            </ProtectedRoute>
          }
        />   
        <Route
          path="/aws/rds/hw/:viewMode"
          element={
            <ProtectedRoute>
              <RdsInstType />
            </ProtectedRoute>
          }
        />              
        <Route
          path="/aws/rds/view-rds/:aid/:riid"
          element={
            <ProtectedRoute>
              <ViewRdsDetails />
            </ProtectedRoute>
          }
        />
        <Route
          path="/jira/meta/list"
          element={
            <ProtectedRoute>
              <ListJiraMeta />
            </ProtectedRoute>
          }
        />
        <Route
          path="/jira/meta/create"
          element={
            <ProtectedRoute>
              <CreateJiraMeta />
            </ProtectedRoute>
          }
        />
        <Route
          path="/jira/meta/edit-m/:jira_id"
          element={
            <ProtectedRoute>
              <EditJiraMeta />
            </ProtectedRoute>
          }
        />
        <Route
          path="/msserver/meta/create"
          element={
            <ProtectedRoute>
              <CreateMSServer />
            </ProtectedRoute>
          }
        />    
        <Route
          path="/msserver/meta/list"
          element={
            <ProtectedRoute>
              <ListMSServer />
            </ProtectedRoute>
          }
        />
        <Route
          path="/msserver/meta/view-ser/:msdbs_id"
          element={
            <ProtectedRoute>
              <ViewMSDetails />
            </ProtectedRoute>
          }
        /> 
        <Route
          path="/msserver/meta/edit-ser/:msdbs_id"
          element={
            <ProtectedRoute>
              <EditMSServer />
            </ProtectedRoute>
          }
        />      
        <Route
          path="/msserver/provision/mssql/database"
          element={
            <ProtectedRoute>
              <CreateMSServerWizard />
            </ProtectedRoute>
          }
        />   
        <Route
          path="/provision/database/jobs"
          element={
            <ProtectedRoute>
              <ListJobs />
            </ProtectedRoute>
          }
        />  
        <Route
          path="/provision/database/view-job/:job_id"
          element={
            <ProtectedRoute>
              <ViewJobProgress />
            </ProtectedRoute>
          }
        />        
        <Route path="*" element={<Page404 />} />
      </Routes>
    </AuthProvider>
  );
}
export default App;
