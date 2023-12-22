import * as React from 'react';
import models from './api/models';
import classNames from 'classnames';
import './App.css'

function App() {
  const [isLoading, setLoading] = React.useState(false);
  const [results, setResults] = React.useState<string[]>();

  const onSubmit: React.FormEventHandler<HTMLFormElement> = React.useCallback(async e => {
    e.preventDefault();
    setLoading(true);

    // @ts-ignore
    const text = e.target['text'].value;
    
    // @ts-ignore
    if (e.target['type'].value === 'cv') {
      const res = await models.get_vacancies_by_cv(text);
      setResults(res.texts);
    } else {
      const res = await models.get_cvs_by_vacancy(text);
      setResults(res.texts);
    }

    setLoading(false);
  }, []);


  return (
    <div className={classNames('app-container', isLoading && '__loading')}>
      {isLoading && (
        <div className="overlay">
          <div className="spinner"/>
        </div>
      )}

      <h1>Демо-приложение поиска вакансий по резюме и резюме по вакансиям</h1>
      <form onSubmit={onSubmit} className="form-container">
        <div>
          Что будете вводить?
          <input type="radio" id="cv" name="type" value="cv" checked/>
          <input type="radio" id="vacancy" name="type" value="vacancy"/>
        </div>

        <div>
          Введите текст:
          <input type="text"/>
        </div>

        <button type='submit'>
          Найти похожие
        </button>
      </form>

      {results && (
        <div>
          <h3>
            Результаты:
          </h3>
          <ul>
            {results.map(result => (
              <li>
                {result}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App
