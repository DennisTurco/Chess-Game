import type { ReactNode } from 'react';
import './common.css';

interface ModalProps {
  open: boolean;
  onClose?: () => void;
  children: ReactNode;
}

export function Modal({ open, onClose, children }: ModalProps) {
  if (!open) return null;
  return (
    <div className="modal-overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose?.()}>
      <div className="modal-card">{children}</div>
    </div>
  );
}
