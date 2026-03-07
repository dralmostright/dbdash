import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import UsersApi from "../../api/UsersApi";
import FormInput from "../../components/forms/FormInput";
import { PageTitle } from "../../components/header/PageTitle";
import { Loading } from "../../components/utils/Loading";

export default function AddUser() {
    const navigate = useNavigate();

    const [validated, setValidated] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const [values, setValues] = useState({
        first_name: "",
        username: "",
        last_name: "",
        email: "",
        password_hash: "",
        confirmpassword: "",
        role: "",
        is_verified: ""
    });

    const pagetitle = {
        title: "Users",
        parent: "Users",
        current: "Add New User"
    }

    const addUserInputs = [
        {
            id: 0,
            name: "username",
            type: "text",
            errorMessage: "Please provide username name.",
            label: "Username",
            required: true,
            pattern: "^[A-Za-z0-9]{3,16}$",
        },
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
        {
            id: 4,
            name: "password_hash",
            type: "password",
            errorMessage: "Password should be 8-20 characters and include at least 1 letter, 1 number and 1 special character!",
            label: "Password",
            required: true,
            pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$`
        },
        {
            id: 5,
            name: "confirmpassword",
            type: "password",
            errorMessage: "Passwords don't match!",
            label: "Confirm Password",
            required: true,
            pattern: values.password_hash,
        },
        {
            id: 6,
            name: "is_verified",
            type: "select",
            label: "User Status",
            required: true,
            errorMessage: "Please select status.",
            options: [
                { value: "", label: "Select Status" },
                { value: "true", label: "Active" },
                { value: "false", label: "Inactive" },
            ]
        },
        {
            id: 7,
            name: "role",
            type: "select",
            label: "User Role",
            required: true,
            errorMessage: "Please select user role.",
            options: [
                { value: "", label: "Select Role" },
                { value: "user", label: "User" },
                { value: "admin", label: "Admin" },
            ]
        },
    ];

    const onChange = (e) => {
        setValues({ ...values, [e.target.name]: e.target.value })
    }

    const handleAddUser = async (e) => {
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
                await UsersApi.create({
                    username: values.username,
                    first_name: values.first_name,
                    last_name: values.last_name,
                    email: values.email,
                    password_hash: values.password_hash,
                    is_verified: values.is_verified,
                    role: values.role,
                });

                setSuccess("User added successfully...");
                setTimeout(() => navigate("/account/listallusers"), 1000);
            } catch (err) {
                await sleep(1000);
                console.error(err);
                setError(err.response?.data?.message || "Adding new user failed. Try again.");
            } finally {
                setLoading(false);
            }
        }
    };
    return (
        <>
            <title> DbDash - Add Users</title>
            <Header />
            <Sidebar />
            <main id="main" className="main">
                <PageTitle pageprops={pagetitle} />
                <section className="section">
                    <div className="row">
                        <div className="col-lg-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">Add New User</h5>
                                    {success && (

                                        <div className="alert alert-success text-center py-2">
                                            {success}
                                        </div>
                                    )}
                                    {error && (

                                        <div className="alert alert-danger alert-dismissible fade show" role="alert">
                                            <i className="bi bi-exclamation-octagon me-1"></i>
                                            {error}
                                            <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                        </div>

                                    )}
                                    <form className={`row g-3 needs-validation ${validated ? "was-validated" : ""}`}
                                        noValidate
                                        onSubmit={handleAddUser}>
                                        {
                                            addUserInputs.map(
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
                                                        Saving...
                                                    </>
                                                ) : (
                                                    "Create User"
                                                )}
                                            </button>

                                        </div>
                                    </form>

                                </div>
                            </div>
                        </div>

                        <div className="col-lg-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">No Labels / Placeholders as labels Form</h5>

                                </div>
                            </div>
                        </div>
                    </div>
                </section>

            </main>
            <Footer />
        </>
    )
}
