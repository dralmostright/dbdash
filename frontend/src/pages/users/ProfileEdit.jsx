import { useState } from "react";
import FormInput from "../../components/forms/FormInput";
import UsersApi from "../../api/UsersApi";
import { DisplayPic } from "./DisplayPic";

export default function ProfileEdit({ user, activetab }) {
    const [validated, setValidated] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const [values, setValues] = useState({
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
    });

    const registerInputs = [
        {
            id: 1,
            name: "first_name",
            type: "text",
            errorMessage: "Please provide your First name.",
            label: "First name",
            required: true,
            pattern: "^[A-Za-z0-9]{3,16}$",
        },
        {
            id: 2,
            name: "last_name",
            type: "text",
            errorMessage: "Please provide your Last name.",
            label: "Last name",
            required: true,
            pattern: "^[A-Za-z0-9]{3,16}$",
        },
        {
            id: 3,
            name: "email",
            type: "email",
            errorMessage: "It should be a valid email address!",
            label: "Email",
            required: true,
            pattern: "^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$"
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
                await UsersApi.changeinfo(user.uid, values);
                setSuccess("Details have been changed successfully!");
            } catch (err) {
                await sleep(1000);
                console.error(err);
                setError(err.response?.data?.message || "Failed to update user details.");
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <div
            className={`tab-pane fade profile-edit pt-3 ${activetab === "edit" ? " active show" : ""
                }`}
        >
            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <h5 className="card-title">Edit Profile</h5>
            <DisplayPic user={user} />

            <form className={`row g-3 needs-validation ${validated ? "was-validated" : ""}`}
                noValidate
                onSubmit={handleRegister}>
                {
                    registerInputs.map(
                        (input) =>
                        (
                            <FormInput key={input.id}
                                {...input}
                                value={values[input.name]}
                                onChange={onChange}
                            />
                        )
                    )
                }

                <div className="col-12">
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
                            "Update"
                        )}
                    </button></div>
            </form>

        </div>
    );
}
