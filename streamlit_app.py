import logging
import matplotlib
import streamlit as st
from app.main import main

# 配置 logging 和 matplotlib
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("running main function")
    main()