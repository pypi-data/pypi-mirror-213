from getajob.vendor.openai import OpenAIAPI


class OpenAIRepository(OpenAIAPI):
    @classmethod
    def extract_keywords(cls, input_text: str, max_tokens: int = 60):
        return cls().text_prompt(
            prompt=f"Extract keywords from this text:\n\n{input_text}",
            max_tokens=max_tokens,
        )

    @classmethod
    def generate_interview_questions(cls, job_name: str, max_tokens: int = 150):
        return cls().text_prompt(
            prompt=f"Create a list of 8 questions for my interview for the job: {job_name}",
            max_tokens=max_tokens,
        )

    @classmethod
    def generate_study_notes(cls, job_name: str, max_tokens: int = 150):
        return cls().text_prompt(
            prompt=f"What are 5 key points I should know when preparing for the job: {job_name}?",
            max_tokens=max_tokens,
        )

    @classmethod
    def factual_answers(cls, question: str, max_tokens: int = 60):
        return cls().text_prompt(prompt=f"Q: {question}\nA:", max_tokens=max_tokens)

    @classmethod
    def grammar_correction(cls, input_text: str, max_tokens: int = 60):
        return cls().text_prompt(
            prompt=f"Correct this to standard English:\n\n{input_text}",
            max_tokens=max_tokens,
        )

    @classmethod
    def ad_text_generation(
        cls,
        job_name: str,
        job_description: str,
        advertise_location: str,
        intended_audience: str,
        max_tokens: int = 100,
    ):
        return cls().text_prompt(
            prompt=f"Write a creative ad to run on {advertise_location} for the position of {job_name} aimed at {intended_audience} using the following job description:\n{job_description}.",
            max_tokens=max_tokens,
        )

    @classmethod
    def cover_letter_help(
        cls,
        job_name: str,
        job_description: str,
        company_name: str,
        max_tokens: int = 100,
    ):
        return cls().text_prompt(
            prompt=f"Write a cover letter for the position of {job_name} at {company_name} using the following job description:\n{job_description}.",
            max_tokens=max_tokens,
        )

    @classmethod
    def resume_help(cls, job_name: str, job_description: str, max_tokens: int = 100):
        return cls().text_prompt(
            prompt=f"Write a resume for the position of {job_name} using the following job description:\n{job_description}.",
            max_tokens=max_tokens,
        )
