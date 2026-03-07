import { Navigate, useParams } from 'react-router';
import { ListRdsRecent } from "./ListRdsRecent";
import { ListRdsAll } from './ListRdsAll';
import { ListRdsUp } from './ListRdsUp';
import { ListRdsDown } from './ListRdsDown';
import { ListRdsMajorEol } from './ListRdsMajorEol';
import { ListRdsMinorEol } from './ListRdsMinorEol';

export function ListRdsInstance() {
    const {viewMode } = useParams();

    if (viewMode === "recent") {
        return <ListRdsRecent />;
      } else if (viewMode === "all") {
        return <ListRdsAll />;
      } else if (viewMode === "up") {
            return <ListRdsUp />
      } else if (viewMode === "down") {
            return <ListRdsDown />            
      } else if (viewMode === "eolmajor") {
        return <ListRdsMajorEol />   
      } else if (viewMode === "eolminor") {
        return <ListRdsMinorEol />                   
      } else {
        return <Navigate to="/404" replace />;
      }

}
