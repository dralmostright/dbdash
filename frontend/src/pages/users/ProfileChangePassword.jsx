import { useState } from "react";
import FormInput from "../../components/forms/FormInput";
import UsersApi from "../../api/UsersApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export default function ProfileChangePassword({ user, activetab }) {
  const [validated, setValidated] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const [values, setValues] = useState({
    password_hash: "",
    new_password_hash: "",
    confirmpassword: "",
  });

  const registerInputs = [
    {
      id: 1,
      name: "password_hash",
      type: "password",
      errorMessage:
        "Password should be 8-20 characters and include at least 1 letter, 1 number and 1 special character!",
      label: "Password",
      required: true,
      pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$`,
    },
    {
      id: 2,
      name: "new_password_hash",
      type: "password",
      errorMessage:
        "Password should be 8-20 characters and include at least 1 letter, 1 number and 1 special character!",
      label: "New Password",
      required: true,
      pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$`,
    },
    {
      id: 3,
      name: "confirmpassword",
      type: "password",
      errorMessage: "Passwords don't match!",
      label: "Confirm Password",
      required: true,
      pattern: values.new_password_hash,
    },
  ];
  const onChange = (e) => {
    setValues({ ...values, [e.target.name]: e.target.value })
}

const handleRegister = async (e) => {
  e.preventDefault();
  const form = e.currentTarget;

  if (!form.checkValidity()) {
      e.stopPropagation();
  }
  function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
  }

  setValidated(true);

  if (form.checkValidity()) {
      setLoading(true); 
      setError("");
      setSuccess("");

      try {
        await sleep(1000);
        await UsersApi.changepassword(user.uid, values);
        setSuccess("Password have been changed successfully!");
      } catch (err) {
          await sleep(1000);
        console.error(err);
        setError(err.response?.data?.message || "Failed to change password.");
      } finally {
        setLoading(false); 

        setValues({
          password_hash: "",
          new_password_hash: "",
          confirmpassword: "",
      });
      setValidated(false);
      form.reset();
      }
    }
  };
  return (
    <div
      className={`pt-3 tab-pane fade ${
        activetab === "password" ? " show active" : ""
      }`} style={{minHeight: "300px"}}
    >
    {error && <ErrorCard message={error} />}
    {success && <div className="alert alert-success">{success}</div>}

      <form className={`row g-3 needs-validation ${validated ? "was-validated" : ""}`}
                                            noValidate
                                            onSubmit={handleRegister}>
        <h5 className="card-title">Change Password</h5>

        {
                                                registerInputs.map(
                                                    (input) =>
                                                    (
                                                        <FormInput key={input.id + "_" + values[input.name]} 
                                                            {...input}
                                                            value={values[input.name]}
                                                            onChange={onChange}
                                                        />
                                                    )
                                                )
                                            }
        <div className="text-center">
        <button
                        className="btn btn-primary w-100"
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <span
                                    className="spinner-border spinner-border-sm me-2"
                                    role="status"
                                    aria-hidden="true"
                                ></span>
                                Updating...
                            </>
                        ) : (
                            "Update Password"
                        )}
                    </button>
        </div>
      </form>
    </div>
  );
}
