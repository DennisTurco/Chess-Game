import type { ButtonHTMLAttributes, ReactNode } from 'react';
import './common.css';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md';
  icon?: ReactNode;
  fullWidth?: boolean;
}

export function Button({
  variant = 'secondary',
  size = 'md',
  icon,
  fullWidth,
  className,
  children,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={['btn', `btn-${variant}`, `btn-${size}`, fullWidth ? 'btn-full' : '', className]
        .filter(Boolean)
        .join(' ')}
      {...rest}
    >
      {icon && <span className="btn-icon">{icon}</span>}
      {children}
    </button>
  );
}
