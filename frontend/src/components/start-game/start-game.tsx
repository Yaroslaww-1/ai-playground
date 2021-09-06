import './index.css';

export const StartGame = ({ onClick } : { onClick: () => void }) => {
  return (
    <button className="start-game" onClick={onClick}>
      Start
    </button>
  )
}
