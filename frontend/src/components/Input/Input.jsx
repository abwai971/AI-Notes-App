import "./Input.css";

function Input({
    label,
    name,
    type = "text",
    value,
    onChange,
    placeholder,
}) {
    return (
        <div className="input-group">
            <label>{label}</label>

            <input
                name={name}
                type={type}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
            />
        </div>
    );
}

export default Input;