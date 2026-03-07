import { Navigate, useParams } from 'react-router';
import { RdsEc2Ebs } from './RdsEc2Ebs';
import { RdsRdsInst } from './RdsRdsInst';

export function RdsInstType() {
    const {viewMode } = useParams();

    if (viewMode === "ebs") {
        return <RdsEc2Ebs />;
      } else if (viewMode === "rds") {
        return <RdsRdsInst />;                  
      } else {
        return <Navigate to="/404" replace />;
      }
}
