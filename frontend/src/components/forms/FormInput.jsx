import { useState } from "react";
const FormInput = (props) => {
    const { label, errorMessage, onChange, ...inputProps } = props;
    const [touched, setTouched] = useState(false);

    if (inputProps.type === "select") {
        const isValid = touched && inputProps.value !== "";

        return (
            <div className="col-12">
                <label className="form-label">{label}</label>
    
                <div className="input-group has-validation">
                    <select
                        {...inputProps}
                        className={`form-select ${
                            touched ? (isValid ? "is-valid" : "is-invalid") : ""
                        }`}
                        onChange={onChange}
                        onBlur={() => setTouched(true)}
                    >
                        {inputProps.options.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
    
                    <div className="invalid-feedback">{errorMessage}</div>
                </div>
            </div>
        );
    }
    else    
    return (
        <div className="col-12">
            <label className="form-label">{label}</label>
            <div className="input-group has-validation">
                <input className={`form-control ${touched ? (inputProps.value.match(inputProps.pattern) ? "is-valid" : "is-invalid") : ""}`} 
                {...inputProps} 
                onChange={onChange}
                onBlur={() => setTouched(true)}
                />
                <div className="invalid-feedback">{errorMessage}</div>
            </div>
        </div>
    )
}

export default FormInput;
