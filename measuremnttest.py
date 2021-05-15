import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

base = automap_base()

base.prepare(engine, reflect=True)

base.classes.keys()


if __name__ == '__main__':
    app.run(debug=True)
