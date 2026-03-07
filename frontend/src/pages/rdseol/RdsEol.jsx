import { Navigate, useParams } from 'react-router';
import { RdsEolPg } from './RdsEolPg';
import { RdsEolApg } from './RdsEolApg';
import { RdsEolMySql } from './RdsEolMySql';
import { RdsEolAMySql } from './RdsEolAMySql';

export function RdsEol() {
    const {viewMode } = useParams();

    if (viewMode === "pg") {
        return <RdsEolPg />;
      } else if (viewMode === "apg") {
        return <RdsEolApg />;   
      } else if (viewMode === "mysql") {
        return <RdsEolMySql />; 
      } else if (viewMode === "amysql") {
        return <RdsEolAMySql />;                                
      } else {
        return <Navigate to="/404" replace />;
      }
}
