from typing import Dict, List, Union

from belvo.resources.base import Resource


class EmploymentRecords(Resource):
    endpoint = "/api/employment-records/"

    def create(
        self,
        link: str,
        attach_pdf: bool = False,
        save_data: bool = True,
        raise_exception: bool = False,
        **kwargs: Dict,
    ) -> Union[List[Dict], Dict]:
        """Retrieve employment records for a link

        Args:
            link (str): The fiscal `link.id` you want specific employment record for.
            attach_pdf (bool, optional): When this is set to `True`, you will receive the PDF as a binary string in the response. Defaults to `False`.
            save_data (bool, optional): Indicates whether or not to persist the data in Belvo. Defaults to `True`.
            raise_exception (bool, optional): Indicates whether to raise an exception or return the API error. Defaults to `False`.

        Returns:
            Dict: The details of the object. For more information on the response from the API, see our api reference
        """

        data = {
            "link": link,
            "attach_pdf": attach_pdf,
            "save_data": save_data,
        }

        return self.session.post(
            self.endpoint, data=data, raise_exception=raise_exception, **kwargs
        )
