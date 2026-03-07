import { useState, forwardRef,useRef, useImperativeHandle } from "react";
import { ServerSelection } from "./ServerSelection";
import { ServerDetails } from "./ServerDetails";

export const StepMounts = forwardRef(({ mounts, setMounts ,serNmounts, setSerNMounts }, ref) => {
  const [serverId, setServerId] = useState("");
  const [errors, setErrors] = useState({
    server: "",
    datadir: "",
    log_dir: "",
  });

  const errorTimeoutRef = useRef(null);

  useImperativeHandle(ref, () => ({
    validate() {
      const newErrors = {
        server: "",
        datadir: "",
        log_dir: "",
      };

      let isValid = true;

      if (!serverId) {
        newErrors.server = "Please select a server";
        isValid = false;
      }

      if (!mounts.mounts?.datadir) {
        newErrors.datadir = "Please select a data directory";
        isValid = false;
      }

      if (!mounts.mounts?.log_dir) {
        newErrors.log_dir = "Please select a log directory";
        isValid = false;
      }

      setErrors(newErrors);

      if (errorTimeoutRef.current) {
        clearTimeout(errorTimeoutRef.current);
      }

      errorTimeoutRef.current = setTimeout(() => {
        setErrors({
          server: "",
          datadir: "",
          log_dir: "",
        });
      }, 2000);

      return isValid;
    },
  }));

  return (
    <div className="card">
      <div className="row gx-3">
        <ServerSelection
          serverId={serverId}
          setServerId={setServerId}
          mounts={mounts}
          setMounts={setMounts}
          errors={errors}
          setErrors={setErrors}
          serNmounts = {serNmounts} 
          setSerNMounts={setSerNMounts}
        />
        <ServerDetails />
      </div>
    </div>
  );
});
