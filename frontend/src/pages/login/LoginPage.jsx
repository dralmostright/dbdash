import { useContext, useState,useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext"
import FormInput from "../../components/forms/FormInput";

export function LoginPage() {
  const { user, login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [validated, setValidated] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // If already logged in, redirect to dashboard
    if (user) {
      navigate("/", { replace: true });
    }
  }, [user, navigate]);  

  const [values, setValues] = useState({
    email: "",
    password_hash: ""
  });

  const loginInputs = [
    {
      id: 1,
      name: "email",
      type: "email",
      errorMessage: "Please enter your email.",
      label: "Email",
      required: true,
    },
    {
      id: 2,
      name: "password_hash",
      type: "password",
      errorMessage: "Password should be at minimum 5 characters!",
      label: "Password",
      required: true,
      pattern: `.{5,}`,
    }
  ];

  const onChange = (e) => {
    setValues({ ...values, [e.target.name]: e.target.value })
  }

  const handleLogin = async (e) => {
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
        await login({
          email: values.email,
          password_hash: values.password_hash,
        });
        setSuccess("Validation successful....!");
        setTimeout(() => navigate("/"), 500);
      } catch (err) {
        await sleep(1000);
        console.error(err);
        setError(err.response?.data?.message || "Login failed. Try again.");
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <>
      <main>
        <title>Login - DbDash</title>
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
                        <h5 className="card-title text-center pb-0 fs-4">Login to Your Account</h5>
                        <p className="text-center small">Enter your username & password to login</p>
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
                      <form
                        className={`row g-3 needs-validation ${validated ? "was-validated" : ""}`}
                        noValidate
                        onSubmit={handleLogin}
                      >

                        {loginInputs.map((input) => (
                          <FormInput key={input.id} {...input} value={values[input.name]} onChange={onChange} />
                        ))}

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
                                Validating...
                              </>
                            ) : (
                              "Login"
                            )}
                          </button>
                        </div>
                        <div className="col-12">
                          <p className="small mb-0">Don't have account? <a href="/auth/register">Create an account</a></p>
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
    </>
  )
}