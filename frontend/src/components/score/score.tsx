import './index.css';

export const Score = ({ score } : { score: number }) => {
  return (
    <h1 className="score">Score: {score}</h1>
  )
}
