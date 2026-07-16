import "./Button.css";

function Button({ children, type = "button", onClick, disabled }) {
    return (
        <button
            className="btn"
            type={type}
            onClick={onClick}
            disabled={disabled}
        >
            {children}
        </button>
    );
}

export default Button;