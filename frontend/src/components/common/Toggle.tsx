import './common.css';

interface ToggleProps {
  checked: boolean;
  onChange: () => void;
  label?: string;
}

export function Toggle({ checked, onChange, label }: ToggleProps) {
  return (
    <label className="toggle">
      <span className={`toggle-track ${checked ? 'on' : ''}`} onClick={onChange}>
        <span className="toggle-thumb" />
      </span>
      {label && <span className="toggle-label">{label}</span>}
    </label>
  );
}
