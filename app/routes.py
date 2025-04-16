from flask import Blueprint, jsonify, request
from app.dto import InvestmentFund
from app.dao import add_fund, get_all_funds, get_fund_by_id, update_fund_performance, delete_fund
from app.exceptions import ResourceNotFoundError, InvalidInputError
import uuid

funds_bp = Blueprint('funds', __name__)

@funds_bp.route('/funds/list', methods=['POST'])
def get_all_funds_endpoint():
    try:
        # Get filtering and pagination parameters from the request body
        filters = request.json or {}
        name_filter = filters.get('name')
        manager_name_filter = filters.get('manager_name')
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 10)

        # Validate pagination parameters
        if not isinstance(page, int) or page <= 0:
            return jsonify({"error": "Invalid 'page' parameter. It must be a positive integer."}), 400
        if not isinstance(per_page, int) or per_page <= 0:
            return jsonify({"error": "Invalid 'per_page' parameter. It must be a positive integer."}), 400

        # Retrieve filtered and paginated funds
        all_funds = [fund.to_dict() for fund in get_all_funds(name_filter, manager_name_filter, page, per_page)]

        return jsonify(all_funds), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve funds", "details": str(e)}), 500

# Endpoint to create a new fund
@funds_bp.route('/funds', methods=['POST'])
def create_fund():
    try:
        data = request.json
        if not data or not all(key in data for key in ['name', 'manager_name', 'description', 'nav', 'creation_date', 'performance']):
            raise InvalidInputError("All fields are required.")

        fund_id = str(uuid.uuid4())
        fund = InvestmentFund(
            fund_id=fund_id,
            name=data['name'],
            manager_name=data['manager_name'],
            description=data['description'],
            nav=data['nav'],
            creation_date=data['creation_date'],
            performance=data['performance']
        )
        add_fund(fund)
        return jsonify(fund.to_dict()), 201
    except InvalidInputError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create fund", "details": str(e)}), 500

# Endpoint to retrieve details of a specific fund using its ID
@funds_bp.route('/funds/<fund_id>', methods=['GET'])
def get_fund(fund_id):
    try:
        fund = get_fund_by_id(fund_id)
        if not fund:
            raise ResourceNotFoundError(f"Fund with ID {fund_id} not found.")
        return jsonify(fund.to_dict()), 200
    except ResourceNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve fund", "details": str(e)}), 500

# Endpoint to update the performance of a fund using its ID
@funds_bp.route('/funds/<fund_id>', methods=['PUT'])
def update_fund_performance_endpoint(fund_id):
    try:
        data = request.json
        if not data or 'performance' not in data:
            raise InvalidInputError("Invalid input. 'performance' field is required.")

        fund = get_fund_by_id(fund_id)
        if not fund:
            raise ResourceNotFoundError(f"Fund with ID {fund_id} not found.")

        update_fund_performance(fund_id, data['performance'])
        updated_fund = get_fund_by_id(fund_id)
        return jsonify(updated_fund.to_dict()), 200
    except InvalidInputError as e:
        return jsonify({"error": str(e)}), 400
    except ResourceNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to update fund performance", "details": str(e)}), 500

# Endpoint to delete a fund using its ID
@funds_bp.route('/funds/<fund_id>', methods=['DELETE'])
def delete_fund_endpoint(fund_id):
    try:
        fund = get_fund_by_id(fund_id)
        if not fund:
            raise ResourceNotFoundError(f"Fund with ID {fund_id} not found.")

        delete_fund(fund_id)
        return jsonify({"message": "Fund deleted successfully"}), 200
    except ResourceNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete fund", "details": str(e)}), 500