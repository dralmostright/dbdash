
import { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext"
import FormInput from "../../components/forms/FormInput";

export function RegisterPage() {

    const { user, register } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        // If already logged in, redirect to dashboard
        if (user) {
          navigate("/", { replace: true });
        }
      }, [user, navigate]);  

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
        confirmpassword: ""
    });

    const registerInputs = [
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
              await register({
                username: values.username,
                first_name: values.first_name,
                last_name: values.last_name,
                email: values.email,
                password_hash: values.password_hash,
              });
      
              setSuccess("Registration successful! Redirecting to login...");
              setTimeout(() => navigate("/auth/login"), 1000); 
            } catch (err) {
                await sleep(1000);
              console.error(err);
              setError(err.response?.data?.message || "Registration failed. Try again.");
            } finally {
              setLoading(false); 
            }
          }
        };

    return (
        <main>
            <div className="container">

                <section className="section register min-vh-100 d-flex flex-column align-items-center justify-content-center py-4">
                    <div className="container">
                        <div className="row justify-content-center">
                            <div className="col-lg-4 col-md-6 d-flex flex-column align-items-center justify-content-center">

                                <div className="d-flex justify-content-center py-4">
                                    <a href="index.html" className="logo d-flex align-items-center w-auto">
                                        <img src="/src/assets/img/logo.png" alt="" />
                                        <span className="d-none d-lg-block">DbDash</span>
                                    </a>
                                </div>

                                <div className="card mb-3">

                                    <div className="card-body">

                                        <div className="pt-4 pb-2">
                                            <h5 className="card-title text-center pb-0 fs-4">Create an Account</h5>
                                            <p className="text-center small">Enter your personal details to create account</p>
                                        </div>
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
                              Creating...
                            </>
                          ) : (
                            "Create Account"
                          )}
                        </button></div>
                                            <div className="col-12">
                                                <p className="small mb-0">Already have an account? <a href="/auth/login">Log in</a></p>
                                            </div>
                                        </form>

                                    </div>
                                </div>

                                <div className="credits">
                                    Designed by <a href="https://dralmostright.github.com/">Suman Adhikari</a>
                                </div>

                            </div>
                        </div>
                    </div>

                </section>

            </div>
        </main>
    )
}
