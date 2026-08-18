from pydantic import ValidationError

from app.models import SummaryResult

def main() -> None:
    try:
        result = SummaryResult(
            title="Python",
            summary="Python 是一种编程语言",
            keywords="Python",   # 故意写错
            questions=[]
        )
        print(result)
    except ValidationError as e:
        print(e)

if __name__ == "__main__":
    main()